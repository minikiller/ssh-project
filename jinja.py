from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))

def renderfile(templateFile, targetFile, dict):
    template = env.get_template(templateFile)
    output_from_parsed_template = template.render(dict)
    print(output_from_parsed_template)

    # to save the results
    with open("./target/"+targetFile, "w") as fh:
        fh.write(output_from_parsed_template)
