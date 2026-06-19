from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

def markdown_to_blocks(markdown):
    block_list = []
    raw_blocks = markdown.split("\n\n")
    for block in raw_blocks:
        sblock = block.strip()
        if sblock:
            block_list.append(sblock)
    return block_list

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")
    total_lines = len(lines)
    code_count = 0
    u_count = 0
    o_count = 1
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    for line in lines:
        if line.startswith(">"):
            code_count += 1
        if line.startswith("- "):
            u_count += 1
        if line.startswith(f"{o_count}. "):
            o_count += 1
    if code_count == total_lines:
        return BlockType.QUOTE
    if u_count == total_lines:
        return BlockType.ULIST
    if o_count == (total_lines + 1):
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    children = []
    for block in block_list:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        if block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        if block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        if block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        if block_type == BlockType.ULIST:
            children.append(ulist_to_html_node(block))
        if block_type == BlockType.OLIST:
            children.append(olist_to_html_node(block))
    return ParentNode("div", children)

def text_to_children(text):
    tnodes = text_to_textnodes(text)
    all_nodes = []
    for node in tnodes:
        all_nodes.append(text_node_to_html_node(node))
    return all_nodes

def paragraph_to_html_node(block):
    parablock = block.replace("\n", " ")
    return ParentNode("p", text_to_children(parablock))

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1:]
    return ParentNode(f"h{level}", text_to_children(text))

def code_to_html_node(block):
    pre_code = block[4:-4]
    new_node = text_node_to_html_node(TextNode(pre_code, TextType.TEXT))
    return ParentNode("pre", [ParentNode("code", [new_node])])

def quote_to_html_node(block):
    quote_lines = block.split("\n")
    all_lines = []
    for line in quote_lines:
        all_lines.append(line.lstrip(">").strip())
    return ParentNode("blockquote", text_to_children(" ".join(all_lines)))

def ulist_to_html_node(block):
    ulist_lines = block.split("\n")
    all_lines = []
    for line in ulist_lines:
        all_lines.append(ParentNode("li", text_to_children(line[2:])))
    return ParentNode("ul", all_lines)

def olist_to_html_node(block):
    olist_lines = block.split("\n")
    all_lines = []
    for line in olist_lines:
        all_lines.append(ParentNode(f"li", text_to_children(line.split(". ", 1)[1])))
    return ParentNode("ol", all_lines)