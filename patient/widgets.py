from django.forms.widgets import MultiWidget, CheckboxInput
from django.utils.safestring import mark_safe

class DentitionWidget(MultiWidget):
    def __init__(self, attrs=None):
        widgets = [CheckboxInput(attrs=attrs) for _ in range(32)]  # 32 teeth for permanent dentition
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.get(str(i), False) for i in range(11, 49) if i not in [19, 20, 29, 30, 39, 40]]
        return [False] * 32

    def render(self, name, value, attrs=None, renderer=None):
        if not isinstance(value, list):
            value = self.decompress(value)
        
        output = []
        teeth_layout = [
            [18,17,16,15,14,13,12,11, 21,22,23,24,25,26,27,28],
            [48,47,46,45,44,43,42,41, 31,32,33,34,35,36,37,38]
        ]
        
        output.append('<div class="dentition-chart">')
        for row in teeth_layout:
            output.append('<div class="teeth-row">')
            for tooth in row:
                index = teeth_layout[0].index(tooth) if tooth in teeth_layout[0] else teeth_layout[1].index(tooth) + 16
                checked = 'checked' if value[index] else ''
                output.append(f'<label><input type="checkbox" name="{name}_{tooth}" value="{tooth}" {checked}>{tooth}</label>')
            output.append('</div>')
        output.append('</div>')
        
        return mark_safe(''.join(output))

class TemporaryDentitionWidget(DentitionWidget):
    def __init__(self, attrs=None):
        widgets = [CheckboxInput(attrs=attrs) for _ in range(20)]  # 20 teeth for temporary dentition
        super(DentitionWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.get(str(i), False) for i in range(51, 86) if i not in range(56, 61) and i not in range(76, 81)]
        return [False] * 20

    def render(self, name, value, attrs=None, renderer=None):
        if not isinstance(value, list):
            value = self.decompress(value)
        
        output = []
        teeth_layout = [
            [55,54,53,52,51, 61,62,63,64,65],
            [85,84,83,82,81, 71,72,73,74,75]
        ]
        
        output.append('<div class="dentition-chart temporary">')
        for row in teeth_layout:
            output.append('<div class="teeth-row">')
            for tooth in row:
                index = teeth_layout[0].index(tooth) if tooth in teeth_layout[0] else teeth_layout[1].index(tooth) + 10
                checked = 'checked' if value[index] else ''
                output.append(f'<label><input type="checkbox" name="{name}_{tooth}" value="{tooth}" {checked}>{tooth}</label>')
            output.append('</div>')
        output.append('</div>')
        
        return mark_safe(''.join(output))