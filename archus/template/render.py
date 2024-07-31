from ..status import HTTPStatus
from ..exceptions import ArchusException
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound


def render_template(template_name, dir=None, **context):
	try:
		"""
		Specially for docs
		"""
		_template_env = Environment(
			loader=FileSystemLoader(dir),
			autoescape=select_autoescape(['html', 'xml'])
		)
		_template = _template_env.get_template(template_name)
		_rendered_content = _template.render(**context).encode('utf-8')
		return _rendered_content
	except TemplateNotFound:
		raise ArchusException(status=HTTPStatus.NOT_FOUND, message="Template not found")

def render_template_as_string(template_name, dir=None, **context):
	try:
		"""
		Specially for docs
		"""
		_template_env = Environment(
			loader=FileSystemLoader(dir),
			autoescape=select_autoescape(['html', 'xml'])
		)
		_template = _template_env.get_template(template_name)
		_rendered_content = _template.render(**context)
		return _rendered_content
	except TemplateNotFound:
		raise ArchusException(status=HTTPStatus.NOT_FOUND, message="Template not found")
