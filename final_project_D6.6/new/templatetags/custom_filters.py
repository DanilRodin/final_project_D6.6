from django import template


register = template.Library()

# выбраные слова для проверки работы фильтра
BAD = ("здоровье", "организм", "природы", "природе", "здоровья")

@register.filter()
def censor(text):
    new_content = text
    for i in BAD:
        new_content = new_content.replace(i,i[:1]+ '*'*(len(i)-1))
    return new_content
