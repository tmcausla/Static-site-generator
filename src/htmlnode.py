class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("fxn not implemented yet")

    def props_to_html(self):
        if self.props is None:
            return ""
        output = ""
        for prop in self.props:
            output += f' {prop}="{self.props[prop]}"'
        return output

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.tag:
            return self.value
        if self.tag == 'br':
            return '<br>'
        if self.tag == 'img':
            return f'<img' + self.props_to_html() + ' />'
        if not self.value:
            raise ValueError("Leaf node to html error: value not provided")
        return f'<{self.tag}' + self.props_to_html() + f'>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError('parent node to html error: parent nodes must have a tag')
        if not self.children:
            raise ValueError('parent node to html error: parent nodes must have children')
        output = f"<{self.tag}" + self.props_to_html() + ">"
        for node in self.children:
            output += node.to_html()
        output += f"</{self.tag}>"
        return output
