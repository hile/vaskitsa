"""
Django project and app template renderer from .j2 jinja files
"""

import shutil

from pathlib import Path

from vaskitsa.tree import Tree

from .file import FileTemplate

DJANGO_TEMPLATES_ROOT = Path(__file__).parent.parent.joinpath('templates/django')


class DjangoPackageRenderer(Tree):
    """
    Django package
    """
    __template_root_path__ = DJANGO_TEMPLATES_ROOT
    __path_replacements__ = []

    @property
    def template_tree(self):
        """
        Return __template_root_path__ as Tree object
        """
        return Tree(self.__template_root_path__)

    @property
    def paths(self):
        """
        Return pairs ofp origin and target paths
        """
        paths = []
        for item in self.template_tree:
            relative_path = item.relative_to(self.template_tree)
            target_path = self.joinpath(self.apply_path_patterns(relative_path))
            paths.append((item, target_path))
        return paths

    def apply_path_patterns(self, path):
        """
        Apply path patterns to relative path
        """
        parts = []
        for part in path.parts:
            part = Path(part)
            if part.suffix == '.j2':
                part = Path(part.stem)
            if str(part) in self.__path_replacements__:
                part = Path(getattr(self, str(part)))
            if str(part.stem) in self.__path_replacements__:
                part = f'{getattr(self, str(part.stem))}{part.suffix}'
            parts.append(str(part))
        return Path(*parts)

    def deploy_file(self, source_path, target_path, overwrite=False):
        """
        Deploy file to target package

        Jinja files are rendered, other files copied as-is
        """
        if not overwrite and target_path.exists():
            return
        if source_path.suffix == '.j2':
            self.render_template(source_path, target_path, overwrite)
        else:
            print(f'copy file {target_path}')
            shutil.copyfile(source_path, target_path)

    def render_template(self, source_path, target_path, overwrite=False):
        """
        Render specified template file to target path
        """
        if not overwrite and target_path.exists():
            return
        FileTemplate(self, source_path).render(target_path)

    def get_template_vars(self, **kwargs):
        """
        Get template variables
        """
        template_vars = {}
        for attr in self.__path_replacements__:
            template_vars[attr] = getattr(self, attr)
        template_vars.update(**kwargs)
        return template_vars

    # pylint: disable=arguments-differ,arguments-renamed
    def create(self, overwrite=False):
        """
        Create app directory structure from filenames in template
        """
        for source_path, target_path in self.paths:
            if source_path.is_dir() and not target_path.is_dir():
                print(f'create directory {target_path}')
                target_path.mkdir(parents=True)

        for source_path, target_path in self.paths:
            if source_path.is_file():
                self.deploy_file(source_path, target_path, overwrite)
