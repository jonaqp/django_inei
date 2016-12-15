import types

from django import template
from django.core.urlresolvers import reverse
from django.template import Node

register = template.Library()


def silence_without_field(fn):
    def wrapped(field, attr):
        if not field:
            return ""
        return fn(field, attr)

    return wrapped


def _process_field_attributes(field, attr, process):
    # split attribute name and value from 'attr:value' string
    params = attr.split(':', 1)
    attribute = params[0]
    value = params[1] if len(params) == 2 else ''

    # decorate field.as_widget method with updated attributes
    old_as_widget = field.as_widget

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        attrs = attrs or {}
        process(widget or self.field.widget, attrs, attribute, value)
        html = old_as_widget(widget, attrs, only_initial)
        self.as_widget = old_as_widget
        return html

    field.as_widget = types.MethodType(as_widget, field)
    return field


@register.filter(name='addcss')
def addcss(field, classes):
    return field.as_widget(attrs={"class": classes})


@register.filter(is_safe=True)
def field_with_classes(value, arg):
    return value.label_tag(attrs={'class': arg})


@register.filter(is_safe=True)
def label_classes(value, classes):
    return value.label_tag(attrs={'class': classes})


@register.filter(name='url_name')
def url_name(parser):
    url_parse = reverse('{0}'.format(str(parser)))
    return url_parse


@register.filter
def make_breadcrumbs(value):
    crumbs = value.split('/')[3:-1]
    home = 'administrator'
    point_breadcrumbs = u"<i class='fa fa-circle'></i>"

    link = u" <li><a href='{0:s}'>Home</a>{1:s}" \
           u"</li>".format(reverse(home + ':' + 'index'),
                           str(point_breadcrumbs))

    for index, name in enumerate(crumbs):
        if len(crumbs) - 1 == index:
            point_breadcrumbs = ''
        link += u" <li><span>{0:s}</span>" \
                u"</li>{1:s}".format(str(name).capitalize(),
                                     str(point_breadcrumbs))

    return link


@register.filter
def make_breadcrumbs_module(value):
    if value:
        crumbs = value.split('/')[3:-1]
        module = str(crumbs[0])
        return module.upper()


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def subtract_date(value, arg):
    result_date = (value - arg).days
    return result_date


@register.simple_tag
def divide_to_int(number_a, number_b):
    try:
        return int(int(number_a) / int(number_b))
    except (ValueError, ZeroDivisionError):
        return None


@register.simple_tag
def percentage(number_a, number_b):
    if number_b > 0:
        return number_a / number_b * 100
    else:
        return 0


@register.filter("append_attr")
@silence_without_field
def append_attr(field, attr):
    def process(widget, attrs, attribute, value):
        if attrs.get(attribute):
            attrs[attribute] += ' ' + value
        elif widget.attrs.get(attribute):
            attrs[attribute] = widget.attrs[attribute] + ' ' + value
        else:
            attrs[attribute] = value

    return _process_field_attributes(field, attr, process)


@register.filter("add_class")
@silence_without_field
def add_class(field, css_class):
    return append_attr(field, 'class:' + css_class)


LABEL_STR_FORMAT = '<label for="{field.auto_id}" {attr}>{field.label}</label>'


@register.tag(name="render_label")
def render_label(parser, token):
    try:
        bits = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r tag requires a form field followed by a list of attributes '
            'and values in the form attr="value"' % token.split_contents()[0])
    tag_name, form_field, form_attr = bits[0], bits[1], bits[2:]

    form_field = parser.compile_filter(form_field)
    return FieldAttributeNode(form_field, form_attr)


class FieldAttributeNode(Node):
    def __init__(self, form_field, form_attr):
        self.form_field = form_field
        self.form_attr = form_attr

        matching = [s for s in self.form_attr if "text=" in s]
        if matching:
            self.field_label = matching[0].split("=")[1].strip("\"")

    def render(self, context):
        bounded_field = self.form_field.resolve(context)
        return LABEL_STR_FORMAT.format(field=bounded_field,
                                       attr=''.join(self.form_attr))


@register.simple_tag
def advanced_label_tag(field):
    """ Return form field label html marked to fill by `*` """
    classes = []
    attrs = {}
    from django.utils.encoding import force_text
    from django.template.defaultfilters import force_escape

    contents = force_text(force_escape(field.label))
    if field.field.required:
        classes.append(u'text-semibold')
        contents = force_text(u'{0:s}'.format(force_escape(field.label)))

    if classes:
        attrs['class'] = u' '.join(classes)

    return field.label_tag(contents=contents, attrs=attrs)