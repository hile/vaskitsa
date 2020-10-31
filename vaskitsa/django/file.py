"""
Templated file for django projects and apps
"""

from vaskitsa.templates.template import TemplateRenderer


class FileTemplate(TemplateRenderer):
    """
    File with template variable substition for django projects
    """
    def __init__(self, component, path):
        super().__init__(path.name, template_directory=path.parent)
        self.component = component
        self.path = path

    def __repr__(self):
        return str(self.path)

    # pylint: disable=arguments-differ
    def render(self, target_path):
        """
        Render template to target path
        """
        kwargs = self.component.get_template_vars()
        print(f'render {target_path}',)
        with open(target_path, 'w') as filedescriptor:
            filedescriptor.write(
                '{}\n'.format(self.template.render(**kwargs))
            )
