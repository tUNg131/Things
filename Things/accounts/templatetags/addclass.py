from django import template

register = template.Library()

@register.filter(name='addclass')
def addclass(field, given_classes_str):
    """
    Provide a method to add class in template
    """
    classes = field.field.widget.attrs.get('class', "")
    given_classes = given_classes_str.split(" ")
    for given_class in given_classes: 
        if classes.find(given_class) == -1:
            # if the given class doesn't exist in the existing classes
            classes = classes + ' ' + given_class
    return field.as_widget(attrs={"class": classes})
