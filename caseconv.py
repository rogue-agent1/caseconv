#!/usr/bin/env python3
"""caseconv - Case converter for text. Zero deps."""
import sys,re
def camel(s):return re.sub(r'[_\-\s]+(\w)',lambda m:m.group(1).upper(),s.lower())
def snake(s):return re.sub(r'([A-Z])',r'_\1',re.sub(r'[\-\s]+','_',s)).lower().strip('_')
def kebab(s):return re.sub(r'([A-Z])',r'-\1',re.sub(r'[_\s]+','-',s)).lower().strip('-')
def title(s):return' '.join(w.capitalize() for w in re.split(r'[_\-\s]+',s))
def const(s):return snake(s).upper()
def main():
    if len(sys.argv)<3:print('Usage: caseconv.py <camel|snake|kebab|title|const> <text>');sys.exit(1)
    fn={'camel':camel,'snake':snake,'kebab':kebab,'title':title,'const':const}[sys.argv[1]]
    print(fn(' '.join(sys.argv[2:])))
if __name__=='__main__':main()
