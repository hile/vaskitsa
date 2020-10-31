"""
Document generator base classes
"""

from ..exceptions import DocumentGeneratorError


class TemplateGenerator:
    """
    Common base class for items linked to template generators
    """
    template_name = None

    @property
    def template_directory(self):
        """
        Return directory for templates from configuration

        By default returns None
        """
        return None

    @property
    def template_loader(self):
        """
        Return jinja2 template loader class

        Must return instance of vaskitsa.templates.Template
        """
        raise NotImplementedError('Property template_loader must be implemented in child class')

    @property
    def template_renderer(self):
        """
        Return template renderer for item
        """
        if self.template_name is None:
            raise DocumentGeneratorError(f'{self.__class__} does not define template_name')
        return self.template_loader(self.template_name, self.template_directory)

    def debug(self, *args):
        """
        Stub for debug messages
        """
        raise NotImplementedError

    def error(self, *args):
        """
        Stub for error callback
        """
        raise NotImplementedError

    def message(self, *args):
        """
        Stub for message callbacck
        """
        raise NotImplementedError

    def get_output_filename(self, directory):
        """
        Get output filename for rendered data
        """
        raise NotImplementedError('get_output_filename() must be implemented in child class')

    def render_template(self):
        """
        Render template
        """
        return self.template_renderer.render(self)

    def generate(self, directory):
        """
        Generate output file by rendering template
        """
        path = self.get_output_filename(directory)

        if not path.parent.is_dir():
            self.debug('create directory', path.parent)
            path.parent.mkdir(parents=True)

        with open(path, 'w') as filedescriptor:
            filedescriptor.write(f'{self.render_template()}\n')
        return path
