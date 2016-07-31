from jinja2.ext import Extension
from jinja2 import nodes


class JinjaBSModalExtension(Extension):
    tags = {'modal'}

    def __init__(self, environment):
        super(JinjaBSModalExtension, self).__init__(environment)
        self.args = {}

    @staticmethod
    def _flatten_output(body):
        flat = []
        for output in body:
            for node in output.nodes:
                flat.append(node)
        return flat

    @staticmethod
    def parse_args(parser):
        params = {}
        parser.stream.expect('lparen')
        while parser.stream.current.type != 'rparen':
            if params:
                parser.stream.expect('comma')
            key = parser.parse_assign_target(name_only=True)
            key.set_ctx('param')
            if parser.stream.skip_if('assign'):
                params[key.name] = parser.parse_expression()
        parser.stream.expect('rparen')
        return params

    def parse(self, parser):
        lineno = next(parser.stream).lineno

        self.args = self.parse_args(parser)

        body = parser.parse_statements(['name:endmodal', 'name:modal_footer'], drop_needle=False)
        if parser.stream.current.type == 'name' and parser.stream.current.value == 'modal_footer':
            next(parser.stream)
            footer = parser.parse_statements(['name:endmodal'], drop_needle=True)
        else:
            footer = None

        result = self.build_wrapper() + self.build_header() + self.build_body(body)
        if footer:
            result.extend(self.build_footer(footer))
        result.extend(self.close_wrapper())
        js = self.build_javascript()
        if js:
            result.extend(self.build_javascript())

        return nodes.Output(result).set_lineno(lineno)

    def build_wrapper(self):
        result = [
            nodes.TemplateData('<div class="modal"')
        ]

        if self.args.get('id'):
            result.extend([
                nodes.TemplateData(' id="'),
                self.args.get('id'),
                nodes.TemplateData('"')
            ])

        result.append(nodes.TemplateData('><div class="modal-dialog"><div class="modal-content">'))

        return result

    def build_header(self):
        result = [nodes.TemplateData("""
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal"><span>&times;</span></button>
        """)]

        if self.args.get('title'):
            result.extend([
                nodes.TemplateData('<h4 class="modal-title">'),
                self.args.get('title'),
                nodes.TemplateData('</h4>'),
            ])

        result.append(nodes.TemplateData('</div>'))

        return result

    def build_body(self, body):
        result = [nodes.TemplateData('<div class="modal-body">')] + \
            self._flatten_output(body) + \
            [nodes.TemplateData('</div>')]
        return result

    def build_footer(self, footer):
        result = [nodes.TemplateData('<div class="modal-footer">')] + \
            self._flatten_output(footer) +\
            [nodes.TemplateData('</div>')]
        return result

    def close_wrapper(self):
        return [nodes.TemplateData('</div></div></div>')]

    def build_javascript(self):
        focus = self.args.get('focus')
        id_ = self.args.get('id')
        if focus and id_:
            result = [
                nodes.TemplateData("""
                <script type="text/javascript">
                    (function() {
                        $('#"""),
                id_,
                nodes.TemplateData("').on('shown.bs.modal', function() { $(this).find('"),
                focus,
                nodes.TemplateData("""').focus() });
                    })();
                    </script>""")]
            return result
        return None

if __name__ == '__main__':
    from jinja2 import Environment

    env = Environment(extensions=[JinjaBSModalExtension])

    template = env.from_string("""
    {% modal(id='modal-full', title='Caption', focus='input') %}
        Modal body here
    {% modal_footer %}
        Modal footer here
    {% endmodal %}
     """)
    html = template.render()

    print(html)
