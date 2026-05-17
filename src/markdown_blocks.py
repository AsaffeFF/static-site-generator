from enum import Enum

from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.ULIST:
            children.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.OLIST:
            children.append(ordered_list_to_html_node(block))
        else:
            raise ValueError(f"invalid block type: {block_type}")
    return ParentNode("div", children)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return list(map(text_node_to_html_node, text_nodes))


def paragraph_to_html_node(block):
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1 :]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block):
    text = block[4:-3]
    raw_text = TextNode(text, TextType.TEXT)
    code = ParentNode("code", [text_node_to_html_node(raw_text)])
    return ParentNode("pre", [code])


def quote_to_html_node(block):
    lines = block.split("\n")
    text = "\n".join(line.lstrip(">").strip() for line in lines)
    return ParentNode("blockquote", text_to_children(text))


def unordered_list_to_html_node(block):
    items = []
    for line in block.split("\n"):
        item_text = line[2:]
        items.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode("ul", items)


def ordered_list_to_html_node(block):
    items = []
    for line in block.split("\n"):
        item_text = line.split(". ", 1)[1]
        items.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode("ol", items)
