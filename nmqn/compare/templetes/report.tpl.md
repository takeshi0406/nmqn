# {{title}}

{% if added + deleted -%}
## addded/deleted

{% for x in added -%}
* \+ [{{ x.url }}]({{ x.url }})
{% endfor -%}
{% for x in deleted -%}
* \- [{{ x.url }}]({{ x.url }})
{% endfor -%}

{%- else -%}

{%- endif -%}

{%- if changed-%}
## changed

{% for x in changed %}
**{{x.url}}**
```css
{{ x.diff }}
```
{%- endfor -%}

{%- else -%}


{%- endif %}
## captures

|  before  |  after  |
|:----|:----|
| ![{{before_path}}]({{before_path}}) | ![{{after_path}}]({{after_path}}) |