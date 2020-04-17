import dis
from types import SimpleNamespace

class Instruction(SimpleNamespace):
    def __init__(self, instruction, in_dict=None):
        if in_dict is not None:
            super().__init__(**in_dict)
        else:
            super().__init__(**{a:b for a,b in zip(dis.Instruction._fields+('was_there', "original_index", "jumps_to"), instruction + ( True, None, None))})

    def is_jumper(self):
        return self.is_abs_jumper() or self.is_rel_jumper()

    def is_rel_jumper(self):
        return self.opcode in dis.hasjrel

    def is_abs_jumper(self):
        return self.opcode in dis.hasjabs

    @classmethod
    def ExtendedArgs(self, value):
        return Instruction(None, in_dict={
            'opcode':144, 'opname':'EXTENDED_ARGS', 'arg':value,
            'argval':value, 'argrepr':value, 'offset':None,
            'starts_line':None, 'is_jump_target':False, 'was_there': False,
            "original_index" : None, "jumps_to": None
        })

    def calculate_offset(self, instructions):
        # Return the offset (rel or abs) to self.jump_to in instructions
        target_loc = 0

        for i, instruction in enumerate(instructions):
            if instruction.was_there and instruction.original_index == self.jumps_to:
                target_loc = i

        target_loc *= 2

        if self.is_abs_jumper():
            return target_loc

        self_loc = 2 * instructions.index(self)

        return target_loc - self_loc - 2
