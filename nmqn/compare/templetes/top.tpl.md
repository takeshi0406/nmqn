# {{name}}

|name|device|changed|added|deleted|
|:----|:----|:----|:----|:----|
{%- for x in pages %}
|[{{x.name}}]({{x.path}})|{{x.device}}|{{x.changed}}|{{x.added}}|{{x.deleted}}|
{%- endfor -%}