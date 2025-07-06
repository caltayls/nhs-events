from jinja2 import Environment, FileSystemLoader
import os
import pandas as pd


def render_html(new_events: pd.DataFrame) -> str:
    pwd = os.getcwd()
    env = Environment(loader=FileSystemLoader(pwd))
    template_path = r"html_templates/new_events_email_template.html"
    template = env.get_template(template_path)
    obj_array = new_events.to_dict(orient='records')
   
    data = {
        'events': obj_array,
        'columns': ['event_name', 'location', 'date', 'website'],
        'count': len(obj_array),
    }
    output = template.render(data)

    return output
