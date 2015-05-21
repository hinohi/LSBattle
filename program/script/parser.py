#coding: utf8
import re
# import  logging

from .common import Block


class Parser(object):
    
    def __init__(self):
        self.re_block = re.compile(r"^(\w+)\s*{$")
        self.re_member = re.compile(r"^(\w+)\s*=\s*(.+)")
        self.n = 0

    def read(self):
        while True:
            self.n += 1
            line = self.f.next() + " "
            line = line[:line.rfind("#")].strip()
            if line and not line[0].startswith("#"):
                return line

    def parse(self, f, **setting):
        self.f = f
        self.n = 0
        self.setting = setting
        while True:
            try:
                line = self.read()
            except StopIteration:
                return
            m = self.re_block.match(line)
            if m is not None:
                name = m.group(1)
                if name in self.setting:
                    # logging.info("reading '%s' block", name)
                    self.read_block(self.setting[name])
                else:
                    # logging.warning("skiping '%s' block", name)
                    self.skip_block()
            else:pass
                # logging.debug("no match line (%i)", self.n)

    def read_block(self, block):
        while True:
            line = self.read()
            if line == "}":return
            while line.endswith("\\"):
                line = line[:-1].strip() + self.read()
            m = self.re_block.match(line)
            if m is not None:
                name = m.group(1)
                if name.startswith("_"):
                    # logging.warning("the block name does not start '_' (%s)", name)
                    continue
                if name in block:
                    next_block = block[name]
                    if "_"+name+"_obj" in block:
                        obj = block["_"+name+"_obj"]()
                        # logging.info("reading '%s' block, that is the obj block", name)
                        self.read_block(obj)
                        next_block.append(obj)
                    elif isinstance(next_block, Block):
                        # logging.info("reading '%s' block", name)
                        self.read_block(next_block)
                    else:pass
                        # logging.debug("%s is not instance of 'Block'", name)
                else:
                    # logging.warning("skiping block, '%s' block does not have '%s' block", block.__class__.__name__, name)
                    self.skip_block()
                continue
            m = self.re_member.match(line)
            if m is not None:
                name, value = m.groups()
                if name.startswith("_"):
                    # logging.warning("the attribute name does not start '_' (%s)", name)
                    continue
                if name in block:
                    if isinstance(block[name], Block):
                        pass
                        # logging.warning("the '%s' is block, not attribute", name)
                    else:
                        func_name = "_"+name+"_func"
                        if func_name in block:
                            func = block[func_name]
                            v = func(value)
                            setattr(block, name, v)
                        else:
                            v = eval(value)
                            setattr(block, name, v)
                        # logging.info("set attribute, %s = %r", name, v)
                else:
                    pass
                    # logging.warning("skiping block, '%s' block does not have '%s'", block.__class__.__name__, name)
            else:
                pass
                # logging.debug("no match line (%i)", self.n)


    def skip_block(self):
        while True:
            line = self.read()
            if line == "}":return
            m = self.re_block.match(line)
            if m is not None:
                self.skip_block()


if __name__ == "__main__":
    f = open("ini")
    p = Parser()
    es = EnemySetting()
    p.parse(f, Enemy=es)
    print es.character[0].name
    print es.character[0].HP
    print es.bullet.color
