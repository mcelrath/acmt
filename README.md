# Authorization Control Merkle Tree (ACMT)

An Authorization Control Merkle Tree (ACMT) is a data structure intended to
represent *authorization* for some particular interaction. We focus here on
authorizing the creation of signatures for Bitcoin and cryptocurrency networks.
For such systems, we assume that there exists a system containing keys used on
the blockchain. Hardware Security Module (HSM) servers are often used for this
purpose. As these keys are extremely sensitive, such systems should be kept
offline to prevent theft. This presents a problem in how the offline system
knows whether a particular request is authorized. Because it's offline it cannot
reach out to authorization servers such as Active Directory, RADIUS, Kerberos,
etc.

The point of an ACMT is to be able to create *bearer* proof that a request is
authorized, via Merkle paths. With data and signatures transported to the
offline server, the necessary authorization data becomes self-validating, and
the offline server can verify that the request is valid without having to reach
out to an external server or database.

The ACMT we propose herein is a Tagged Merkle Tree, with levels in the tree
representing different kinds of operators: owners, admins, operators, and
customers/users. All nodes in the tree contain a public key as part of the tag,
and additionally, the remaining tag applied to that node contains semantic rules
about what the owner of that public key can authorize. For nodes near the root
(owner/admin nodes) this includes the ability to create child nodes (e.g.
adding operators or customers). For leaf nodes, the tag contains rules about
what kind of interactions can be authorized by the owner of that public key.
(e.g. transactions less than 10 BTC in value)

In order to create new child nodes, they must be authorized by the next level
up via a cryptographic signature using the public key in the parent node. These
signatures can be stored in the tree itself, or can be folded into a separate
tree with the same structure, that must be presented alongside a Merkle path for
the ACMT.

After creating the ACMT and populating it, the offline server can validate a
Merkle branch, but it has to know that the entire tree is valid and hasn't been
replaced. Thus the offline server must have knowledge of the root of the tree,
but when the tree is updated it must know that the new tree is valid and that
it's looking at the latest state and not some old state with revoked keys.
(Again it's offline and cannot use e.g. CRL's to determine if authorization has
been revoked) For this, we propose to timestamp the root into bitcoin, which
acts as both a clock and a means to achieve immutability of the tree.

Time-stamping by placing the root in Bitcoin is not sufficient (a la
OpenTimestamps) since multiple versions of the ACMT could be time-stamped.
What's required instead is a time-stamping mechanism that additionally adds a
linearly ordered history, disallowing multiple versions from existing. One
implementation that does this is mainstay.xyz. It can also be done by making a
chain of transactions on bitcoin where the first output of that transaction is
spent whenever the tree is updated. One must then prove to the offline server
that a given slot in Mainstay has a particular value as of the latest block
hash, or that a particular UTXO is unspent as of the latest block hash.

Once a linearly-ordered history is created, Bearer proof of the blockchain state
can be created using only block headers and Non-Interactive Proofs of Proof of
Work (NiPoWPoW), and must accompany an authorization request using a Merkle
branch of the ACMT. The offline server can verify this linear chain of history,
verify the timestamp of the latest block hash against its own clock, and verify
the proof of work in the headers, ensuring that using old (revoked) state is
impossible as long as Bitcoin continues to create blocks, and creating a false
history is as computationally expensive as a 51% attack on bitcoin.

The ACMT aslo has the advantage that authorization signature can be collected
slowly over time and aggregated by a separate, online system. Because this
system should not have any of the keys needed to create signatures for the
leaves, it cannot create a fraudulent proof and is only responsible for
validating the signatures and tags, and packaging the data for transport to the
offline signing server.

Because the proof of authorization is self-validating, a complete authorization
Merkle branch and its corresponding proof can be additionally time-stamped into
bitcoin. This is valuable in the event of a dispute or fraud, to prove that an
authorization happened as prescribed.
