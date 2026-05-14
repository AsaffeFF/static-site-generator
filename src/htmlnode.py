class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None or len(self.props) <= 0:
            return ''
        props_list = [f"${key}=\"${value}\"" for key, value in self.props.items()]
        return ' '.join(props_list)

    def __repr__(self):
        return f"${self.tag}\n${self.value}\n${self.children}\n${self.props}"
    
