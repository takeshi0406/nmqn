# report

|name|changed|added|deleted|
|:----|:----|:----|:----|
{% for x in diffs %}
|[{{x.name}}]({{x.path}})|{{x.changed}}|{{x.added}}|{{x.deleted}}|
{%- endfor -%}