
class Merkle:
    def __init__(self, pubkey):
        """ Create a new ACMT with root key <pubkey> """
        self.
        pass

    def root(self):
        """ compute the Merkle root for the ACMT """
        pass

    def branch(self, leafid):
        """ Compute a Merkle branch for a given leaf. """
        pass

    def branchproof(self):
        """ Get """
        pass

    def validate(self, branch, proof):
        """ Given a Merkle <branch> of this tree (created by branchproof()) and
            a list of signatures <proof>, validate that the action is authorized
            by checking signatures and validating tag rules. """
        pass

    def 
