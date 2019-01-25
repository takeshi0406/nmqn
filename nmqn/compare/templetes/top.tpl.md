# report

|name|changed|added|deleted|
|:----|:----|:----|:----|
{% for x in pages %}
|[{{x.name}}]({{x.path}})|{{x.changed}}|{{x.added}}|{{x.deleted}}|
{%- endfor -%}