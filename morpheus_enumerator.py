#!/usr/bin/env python

import spec as S
from interpreter import PostOrderInterpreter, InterpreterError
from enumerator import SmtEnumerator
from synthesizer import ExampleConstraintSynthesizer, Example
import rpy2.robjects as robjects
from logger import get_logger

logger = get_logger('tyrell')

robjects.r('''
    library(dplyr)
    library(tidyr)
   ''')

## Common utils.
def get_collist(sel):
    sel_str = ",".join(sel)
    return "c(" + sel_str + ")"

class MorpheusInterpreter(PostOrderInterpreter):
    ## Concrete interpreter
    def eval_ColInt(self, v):
        return int(v)

    def eval_ColList(self, v):
        return v

    def eval_const(self, node, args):
        return args[0]

    def eval_select(self, node, args):
        _script = 'select({table}, {cols})'.format(
                   table=args[0], cols=get_collist(args[1]))
        try:
            ret_val = robjects.r(_script)
            return ret_val
        except:
            raise InterpreterError(
                'Position must be between 0 and n: {}'.format(node))

    def eval_unite(self, node, args):
        _script = 'unite({table}, TMP, {col1}, {col2})'.format(
                  table=args[0], col1=str(args[1]), col2=str(args[2]))
        try:
            ret_val = robjects.r(_script)
            return robjects.r(_script)
        except:
            raise InterpreterError(
                'Position must be between 0 and n: {}'.format(node))

    def eval_filter(self, node, args):
        _script = '{table} %>% filter(.[[{col}]] {op} {const})'.format(
                  table=args[0], op=args[1], col=str(args[2]), const=str(args[3]))
        try:
            ret_val = robjects.r(_script)
            return robjects.r(_script)
        except:
            raise InterpreterError(
                'filter is not type-checked: {}'.format(_script))

    def eval_separate(self, node, args):
        _script = 'separate({table}, {col1}, c("TMP1", "TMP2"))'.format(
                  table=args[0], col1=str(args[1])) 
        try:
            ret_val = robjects.r(_script)
            return robjects.r(_script)
        except:
            raise InterpreterError(
                'separate is not type-checked: {}'.format(node))

    def eval_spread(self, node, args):
        _script = 'spread({table}, {col1}, {col2})'.format(
                  table=args[0], col1=str(args[1]), col2=str(args[2]))
        try:
            ret_val = robjects.r(_script)
            return robjects.r(_script)
        except:
            raise InterpreterError(
                'spread is not type-checked: {}'.format(node))

    def eval_gather(self, node, args):
        _script = 'gather({table}, KEY, VALUE, {cols})'.format(
                   table=args[0], cols=get_collist(args[1]))
        try:
            ret_val = robjects.r(_script)
            return robjects.r(_script)
        except:
            raise InterpreterError(
                'gather is not type-checked: {}'.format(node))

    def eval_group_by(self, node, args):
        _script = 'group_by({table}, {cols})'.format(
                   table=args[0], cols=get_collist(args[1]))
        try:
            ret_val = robjects.r(_script)
            return robjects.r(_script)
        except:
            raise InterpreterError(
                'group_by is not type-checked: {}'.format(node))

    def eval_summarise(self, node, args):
        _script = '{table} %>% summarise(TMP = {aggr} (.[[{col}]]))'.format(
                  table=args[0], aggr=str(args[1]), col=str(args[2]))
        try:
            ret_val = robjects.r(_script)
            return robjects.r(_script)
        except:
            raise InterpreterError(
                'summarise is not type-checked: {}'.format(_script))

    def eval_mutate(self, node, args):
        _script = '{table} %>% mutate(TMP=.[[{col1}]] {op} .[[{col2}]])'.format(
                  table=args[0], op=args[1], col1=str(args[2]), col2=str(args[3]))
        try:
            ret_val = robjects.r(_script)
            return robjects.r(_script)
        except:
            raise InterpreterError(
                'mutate is not type-checked: {}'.format(_script))

    def eval_inner_join(self, node, args):
        _script = 'inner_join({t1}, {t2})'.format(
                  t1=args[0], t2=args[1])
        try:
            ret_val = robjects.r(_script)
            return robjects.r(_script)
        except:
            raise InterpreterError(
                'inner_join is not type-checked: {}'.format(_script))

    ## Abstract interpreter
    def apply_row(self, val):
        df = val
        if isinstance(val, str):
            df = robjects.r(val)
        ## df: rpy2.robjects.vectors.DataFrame

        return df.nrow

    def apply_col(self, val):
        df = val
        if isinstance(val, str):
            df = robjects.r(val)

        return df.ncol


def main():

    ##### Input-output constraint
    benchmark1_input = robjects.r('''
    dat <- read.table(text="
    round var1 var2 nam        val
    round1   22   33 foo 0.16912201
    round2   11   44 foo 0.18570826
    round1   22   33 bar 0.12410581
    round2   11   44 bar 0.03258235
    ", header=T)
    dat
   ''')

    benchmark1_output = robjects.r('''
    dat2 <- read.table(text="
    nam val_round1 val_round2 var1_round1 var1_round2 var2_round1 var2_round2
    bar  0.1241058 0.03258235          22          11          33          44
    foo  0.1691220 0.18570826          22          11          33          44
    ", header=T)
    dat2
   ''')

    logger.info('Parsing Spec...')
    spec = None
    with open('example/morpheus.tyrell', 'r') as f:
        m_spec_str = f.read()
        spec = S.parse(m_spec_str)
    logger.info('Parsing succeeded')

    logger.info('Building synthesizer...')
    synthesizer = ExampleConstraintSynthesizer(
        #loc: # of function productions
        enumerator=SmtEnumerator(spec, depth=2, loc=1),
        # enumerator=SmtEnumerator(spec, depth=3, loc=2),
        interpreter=MorpheusInterpreter(),
        examples=[
            Example(input=['dat'], output=benchmark1_output),
        ]
    )
    logger.info('Synthesizing programs...')

    prog = synthesizer.synthesize()
    if prog is not None:
        logger.info('Solution found: {}'.format(prog))
    else:
        logger.info('Solution not found!')


if __name__ == '__main__':
    logger.setLevel('DEBUG')
    main()