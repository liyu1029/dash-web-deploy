from dash import dcc

def Dropdown(options, value, **kwargs):
    if 'className' in kwargs:
        input_className = kwargs.pop('className')
        className = "customDropdown " + input_className
    else:
        className = "customDropdown"
    return dcc.Dropdown(options, value, className=className, **kwargs)

# def Dropdown(**kwargs):
#     style = kwargs.pop('style')
#     style_with_defaults = dict({'width': '50px'}, **style)
#     return dcc.Dropdown(style=style_with_defaults, **kwargs)


