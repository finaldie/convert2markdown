#!/usr/bin/python

import sys
import getopt
import xml.etree.cElementTree as ET

# Util
def get_subtree(tree, name):
    for subtree in tree.iter(tag='sectiondef'):
        if subtree.attrib['kind'] == name:
            return subtree

def get_prefix(level):
    prefix = ""
    for i in range(level):
        prefix += "   "

    return prefix

def parse_list(list_tree, level):
    print list_tree.text or ""

    for elem in list_tree:
        if elem.tag == "itemizedlist":
            parse_item_list(elem, level)
        elif elem.tag == "orderedlist":
            parse_order_list(elem, level)

def parse_order_list(order_list, level):
    for elem in order_list:
        if elem.tag == "listitem":
            print "%s1. " % (get_prefix(level)),
            parse_list(elem[0], level + 1)

def parse_item_list(list_items, level):
    for elem in list_items:
        if elem.tag == "listitem":
            print "%s* " % (get_prefix(level)),
            parse_list(elem[0], level + 1)

#===============================================================================
def parse_xml_file(xml_file):
    tree = ET.parse(xml_file)
    return tree

def convert_functree2markdown(func_tree, level):
    for memberdef in func_tree:
        # parse the memberdef child, this is section including all function
        # informations
        parse_memberdef(memberdef, level)

def parse_memberdef(memberdef, level):
    function_name = ""
    function_definition = ""
    brief = ""

    for elem in memberdef:
        if elem.tag == "definition":
            function_definition += elem.text
        elif elem.tag == "argsstring":
            function_definition += elem.text
        elif elem.tag == "name":
            function_name = elem.text
        elif elem.tag == "briefdescription":
            if len(elem):
                brief = elem[0].text

    # start to print the members of a function
    print "## %s" % (function_name)
    print "```c\n%s\n```" % (function_definition)
    print "* brief: %s" % (brief)

    for elem in memberdef:
        if elem.tag == "detaileddescription":
            if len(elem):
                # it only have one child <para>, if the child exist, dump the
                # detail information
                parse_detail(elem[0], level)

    print ""

def parse_detail(detail_tree, level):
    for elem in detail_tree:
        if elem.tag == "parameterlist" and elem.attrib['kind'] == "param":
            parse_params(elem, level)
        elif elem.tag == "simplesect" and elem.attrib['kind'] == "return":
            parse_simplesect("return", elem, level)
        elif elem.tag == "simplesect" and elem.attrib['kind'] == "note":
            parse_simplesect("note", elem, level)

def parse_params(params_tree, level):
    for elem in params_tree:
        if elem.tag == "parameteritem":
            parse_param_item(elem, level)

def parse_param_item(param_item, level):
    for elem in param_item:
        if elem.tag == "parameternamelist":
            print "* param: `%s`" % (elem[0].text),
        elif elem.tag == "parameterdescription":
            # no child, dump the text directly
            if len(elem[0]) == 0:
                if elem[0].text:
                    print " %s" % (elem[0].text)
            else:
                # move to itemizedlist node
                parse_list(elem[0], level + 1)

def parse_simplesect(title, tree, level):
    print "* %s:" % (title),

    # move to <para> node
    if len(tree[0]) == 0:
        if tree[0].text:
            print " %s" % (tree[0].text)
    else:
        parse_list(tree[0], level + 1)

def usage():
    print "usage: xml2markdown.py -f target.xml [-h]"

if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        exit(1)

    xml_file = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:")

        for op, value in opts:
            if op == "-h":
                sys.exit(0)
            elif op == "-f":
                xml_file = value

    except Exception, e:
        print "Fatal: " + str(e)
        usage()
        sys.exit(1)

    tree = parse_xml_file(xml_file)
    func_tree = get_subtree(tree, "func")

    if func_tree:
        convert_functree2markdown(func_tree, 0)
