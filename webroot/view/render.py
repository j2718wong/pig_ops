__author__ = "Jack Wong, jack.wong@erg.com.hk, neoaspilet1@gmail.com"
__date__ = "$2015-02-09 10:00:00$"


from mako.template import Template



class PageElement:
    def __init__(self, div_id = None, div_class = None):
        self.div_id = div_id
        self.div_class = div_class

    def pre(self):
        text = "<div"
        if self.div_id is not None:
            text += " id=\"" + self.div_id + "\""
        if self.div_class is not None:
            text += " class=\"" + self.div_class + "\""
        return text + ">"

    def post(self):
        return "</div>"


class RenderText:
    def __init__(self, render_text):
        self.render_text = render_text

    def render(self):
        return self.render_text


class RenderFunction:
    def __init__(self, render_function, arguments = None):
        self.render_function = render_function
        self.arguments = arguments

    def render(self):
        if self.arguments is not None:
            return self.render_function(self.arguments)
        else:
            return self.render_function()

        master_page = RenderNode()

        rn = RenderNode(template_filename = "")
        master_page.add(rn)

        master_page.render()


                
class RenderNode:
    def __init__(self, subnodes = None, page_element = None,
                function = None, function_parameters = None,
                text = None, template = None, template_filename = None,
                template_parameters = {}):
        self.page_element = page_element
        if subnodes is not None:
            self.subnodes = subnodes
        else:
            self.subnodes = []
        if function is not None:
            self.add_function(function, function_parameters)
        if text is not None:
            self.add_text(text)
        if template is not None:
            self.add_text(template.render(**template_parameters))
        if template_filename is not None:
            self.add_text(Template(filename = template_filename).render(**template_parameters))

    def add(self, subnode):
        self.subnodes.append(subnode)

    def add_function(self, render_function, arguments = None):
        self.subnodes.append(RenderFunction(render_function, arguments))

    def add_text(self, render_text):
        self.subnodes.append(RenderText(render_text))

    def render(self):
        text = ""
        if self.page_element is not None:
            text += self.page_element.pre()
        if len(self.subnodes) > 0:
            for subnode in self.subnodes:
                text += subnode.render()
        if self.page_element is not None:
            text += self.page_element.post()
        return text



class TopRenderNode:
    def __init__(self, render_node = None, scripts = [], css = [], text = None):
                    
        if render_node is None:
            if text is not None:
                self.render_node = RenderNode(text = text)
        else:
            self.render_node = render_node

        self.scripts    = scripts
        self.css        = css


    def set_render_node(self, render_node):
        self.render_node = render_node


    def render(self, controller):

        render_index = RenderNode()

        render_main = RenderNode(page_element = PageElement(div_id = "main"))
        if self.render_node is not None:
            render_main.add(self.render_node)

        render_index.add(render_main)

        # Return page
        template_index = Template(filename = 'templates/index.html',
                        input_encoding = 'utf-8', output_encoding = 'utf-8')

        
        return template_index.render(
                    main            = render_index.render(),
                    scripts         = self.scripts,
                    cache           = False,
                    controller      = controller,
                    css             = self.css
                    )