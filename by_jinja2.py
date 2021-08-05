import jinja2


def render_html(names):
    """
    Render html page using jinja
    """
    template_loader = jinja2.FileSystemLoader(searchpath="./")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "index.html"
    template = template_env.get_template(template_file)
    output_text = template.render(
        names=names,
        # address=row.Address,
        # date=get_date(),
        # invoice=row.Invoice,
        # item=row.Item,
        # amount=row.Cost
    )

    # html_path = f'{row.Name}.html'
    html_path = f'haha.html'
    html_file = open(html_path, 'w')
    html_file.write(output_text)
    html_file.close()


render_html(['forhad', 'mahabub'])


