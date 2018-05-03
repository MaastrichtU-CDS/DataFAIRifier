import ipywidgets as widgets

class ResultWidget:
    def __init__(self, result, description):
        self.result = result

        self.x_widget = widgets.Dropdown(
            options=result.columns.values,
            value=result.columns.values[0],
            description='x'+description,
            disabled=False,
        )

        self.y_widget = widgets.Dropdown(
            options=result.columns.values,
            value=result.columns.values[1],
            description='y'+description,
            disabled=False,
        )
                    
        self.x_widget.observe(self.update_y_value, 'value')
        self.y_widget.observe(self.update_x_value, 'value')

    def prevent_value_clash(self, widget1, widget2):
        if widget1.value == widget2.value:
            if widget1.value == self.result.columns.values[0]:
                widget2.value = self.result.columns.values[1]
            else:
                widget2.value = self.result.columns.values[0]

    def update_y_value(self, *args):
        self.prevent_value_clash(self.x_widget, self.y_widget)

    def update_x_value(self, *args):
        self.prevent_value_clash(self.y_widget, self.x_widget)
