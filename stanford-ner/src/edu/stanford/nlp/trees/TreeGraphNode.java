package edu.stanford.nlp.trees;

import java.io.StringReader;
import java.util.List;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.Label;
import edu.stanford.nlp.ling.LabelFactory;
import edu.stanford.nlp.util.StringUtils;

/**
 * <p>
 * A <code>TreeGraphNode</code> is simply a
 * {@link Tree <code>Tree</code>}
 * with some additional functionality.  For example, the
 * <code>parent()</code> method works without searching from the root.
 * Labels are always assumed to be
 * {@link CoreLabel <code>CoreLabel</code>}
 *
 * <p>This class makes the horrible mistake of changing the semantics of
 * equals and hashCode to go back to "==" and System.identityHashCode,
 * despite the semantics of the superclass's equality.</p>
 *
 * @author Bill MacCartney
 */
public class TreeGraphNode extends Tree implements HasParent {

  /**
   * Label for this node.
   */
  protected CoreLabel label;

  /**
   * Parent of this node.
   */
  protected TreeGraphNode parent; // = null;


  /**
   * Children of this node.
   */
  protected TreeGraphNode[] children = ZERO_TGN_CHILDREN;

  /**
   * The {@link GrammaticalStructure <code>GrammaticalStructure</code>} of which this
   * node is part.
   */
  protected GrammaticalStructure tg;

  /**
   * A leaf node should have a zero-length array for its
   * children. For efficiency, subclasses can use this array as a
   * return value for children() for leaf nodes if desired. Should
   * this be public instead?
   */
  protected static final TreeGraphNode[] ZERO_TGN_CHILDREN = new TreeGraphNode[0];

  private static LabelFactory mlf = CoreLabel.factory();

  /**
   * Create a new empty <code>TreeGraphNode</code>.
   */
  public TreeGraphNode() {
  }

  /**
   * Create a new <code>TreeGraphNode</code> with the supplied
   * label.
   *
   * @param label the label for this node.
   */
  public TreeGraphNode(Label label) {
    this.label = (CoreLabel) mlf.newLabel(label);
  }

  /**
   * Create a new <code>TreeGraphNode</code> with the supplied
   * label and list of child nodes.
   *
   * @param label    the label for this node.
   * @param children the list of child <code>TreeGraphNode</code>s
   *                 for this node.
   */
  public TreeGraphNode(Label label, List<Tree> children) {
    this(label);
    setChildren(children);
  }

  /**
   * Create a new <code>TreeGraphNode</code> having the same tree
   * structure and label values as an existing tree (but no shared
   * storage).
   * @param t     the tree to copy
   * @param graph the graph of which this node is a part
   */
  public TreeGraphNode(Tree t, GrammaticalStructure graph) {
    this(t, (TreeGraphNode) null);
    this.setTreeGraph(graph);
  }

  // XXX TODO it's not really clear what graph the copy should be a part of
  public TreeGraphNode(TreeGraphNode t) {
    this(t, t.parent);
    this.setTreeGraph(t.treeGraph());
  }

  /**
   * Create a new <code>TreeGraphNode</code> having the same tree
   * structure and label values as an existing tree (but no shared
   * storage).  Operates recursively to construct an entire
   * subtree.
   *
   * @param t      the tree to copy
   * @param parent the parent node
   */
  protected TreeGraphNode(Tree t, TreeGraphNode parent) {
    this.parent = parent;
    Tree[] tKids = t.children();
    int numKids = tKids.length;
    children = new TreeGraphNode[numKids];
    for (int i = 0; i < numKids; i++) {
      children[i] = new TreeGraphNode(tKids[i], this);
      if (t.isPreTerminal()) { // add the tags to the leaves
        children[i].label.setTag(t.label().value());
      }
    }
    this.label = (CoreLabel) mlf.newLabel(t.label());
  }

  /**
   * Implements equality for <code>TreeGraphNode</code>s.  Unlike
   * <code>Tree</code>s, <code>TreeGraphNode</code>s should be
   * considered equal only if they are ==.  <i>Implementation note:</i>
   * TODO: This should be changed via introducing a Tree interface with the current Tree and this class implementing it, since what is done here breaks the equals() contract.
   *
   * @param o The object to compare with
   * @return Whether two things are equal
   */
  @Override
  public boolean equals(Object o) {
    return o == this;
  }

  @Override
  public int hashCode() {
    return System.identityHashCode(this);
  }

  /**
   * Returns the label associated with the current node, or null
   * if there is no label.
   *
   * @return the label of the node
   */
  @Override
  public CoreLabel label() {
    return label;
  }

  /**
   * Sets the label associated with the current node.
   *
   * @param label the new label to use.
   */
  public void setLabel(final CoreLabel label) {
    this.label = label;
  }

  /**
   * Get the index for the current node.
   */
  public int index() {
    return label.index();
  }

  /**
   * Set the index for the current node.
   */
  protected void setIndex(int index) {
    label.setIndex(index);
  }

  /**
   * Get the parent for the current node.
   */
  @Override
  public TreeGraphNode parent() {
    return parent;
  }

  /**
   * Set the parent for the current node.
   */
  public void setParent(TreeGraphNode parent) {
    this.parent = parent;
  }

  /**
   * Returns an array of the children of this node.
   */
  @Override
  public TreeGraphNode[] children() {
    return children;
  }

  /**
   * Sets the children of this <code>TreeGraphNode</code>.  If
   * given <code>null</code>, this method sets
   * the node's children to the canonical zero-length Tree[] array.
   *
   * @param children an array of child trees
   */
  @Override
  public void setChildren(Tree[] children) {
    if (children == null || children.length == 0) {
      this.children = ZERO_TGN_CHILDREN;
    } else {
      if (children instanceof TreeGraphNode[]) {
        this.children = (TreeGraphNode[]) children;
      } else {
        this.children = new TreeGraphNode[children.length];
        for (int i = 0; i < children.length; i++) {
          this.children[i] = (TreeGraphNode)children[i];
        }
      }
    }
  }

  /** {@inheritDoc} */
  @Override
  public void setChildren(List<? extends Tree> childTreesList) {
    if (childTreesList == null || childTreesList.isEmpty()) {
      setChildren(ZERO_TGN_CHILDREN);
    } else {
      int leng = childTreesList.size();
      TreeGraphNode[] childTrees = new TreeGraphNode[leng];
      childTreesList.toArray(childTrees);
      setChildren(childTrees);
    }
  }

  /**
   * Get the <code>GrammaticalStructure</code> of which this node is a
   * part.
   */
  protected GrammaticalStructure treeGraph() {
    return tg;
  }

  /**
   * Set pointer to the <code>GrammaticalStructure</code> of which this node
   * is a part.  Operates recursively to set pointer for all
   * descendants too.
   */
  protected void setTreeGraph(GrammaticalStructure tg) {
    this.tg = tg;
    for (TreeGraphNode child : children) {
      child.setTreeGraph(tg);
    }
  }

  /**
   * Uses the specified {@link HeadFinder <code>HeadFinder</code>}
   * to determine the heads for this node and all its descendants,
   * and to store references to the head word node and head tag node
   * in this node's {@link CoreLabel <code>CoreLabel</code>} and the
   * <code>CoreLabel</code>s of all its descendants.<p>
   * <p/>
   * Note that, in contrast to {@link Tree#percolateHeads
   * <code>Tree.percolateHeads()</code>}, which assumes {@link
   * edu.stanford.nlp.ling.CategoryWordTag
   * <code>CategoryWordTag</code>} labels and therefore stores head
   * words and head tags merely as <code>String</code>s, this
   * method stores references to the actual nodes.  This mitigates
   * potential problems in sentences which contain the same word
   * more than once.
   *
   * @param hf The headfinding algorithm to use
   */
  @Override
  public void percolateHeads(HeadFinder hf) {
    if (isLeaf()) {
      TreeGraphNode hwn = headWordNode();
      if (hwn == null) {
        setHeadWordNode(this);
      }
    } else {
      for (Tree child : children()) {
        child.percolateHeads(hf);
      }
      TreeGraphNode head = safeCast(hf.determineHead(this,parent));
      if (head != null) {

        TreeGraphNode hwn = head.headWordNode();
        if (hwn == null && head.isLeaf()) { // below us is a leaf
          setHeadWordNode(head);
        } else {
          setHeadWordNode(hwn);
        }

        TreeGraphNode htn = head.headTagNode();
        if (htn == null && head.isLeaf()) { // below us is a leaf
          setHeadTagNode(this);
        } else {
          setHeadTagNode(htn);
        }

      } else {
        System.err.println("Head is null: " + this);
      }
    }
  }

  /**
   * Return the node containing the head word for this node (or
   * <code>null</code> if none), as recorded in this node's {@link
   * CoreLabel <code>CoreLabel</code>}.  (In contrast to {@link
   * edu.stanford.nlp.ling.CategoryWordTag
   * <code>CategoryWordTag</code>}, we store head words and head
   * tags as references to nodes, not merely as
   * <code>String</code>s.)
   *
   * @return the node containing the head word for this node
   */
  public TreeGraphNode headWordNode() {
    TreeGraphNode hwn = safeCast(label.get(TreeCoreAnnotations.HeadWordAnnotation.class));
    if (hwn == null || (hwn.treeGraph() != null && !(hwn.treeGraph().equals(this.treeGraph())))) {
      return null;
    }
    return hwn;
  }

  /**
   * Store the node containing the head word for this node by
   * storing it in this node's {@link CoreLabel
   * <code>CoreLabel</code>}.  (In contrast to {@link
   * edu.stanford.nlp.ling.CategoryWordTag
   * <code>CategoryWordTag</code>}, we store head words and head
   * tags as references to nodes, not merely as
   * <code>String</code>s.)
   *
   * @param hwn the node containing the head word for this node
   */
  private void setHeadWordNode(final TreeGraphNode hwn) {
    label.set(TreeCoreAnnotations.HeadWordAnnotation.class, hwn);
  }

  /**
   * Return the node containing the head tag for this node (or
   * <code>null</code> if none), as recorded in this node's {@link
   * CoreLabel <code>CoreLabel</code>}.  (In contrast to {@link
   * edu.stanford.nlp.ling.CategoryWordTag
   * <code>CategoryWordTag</code>}, we store head words and head
   * tags as references to nodes, not merely as
   * <code>String</code>s.)
   *
   * @return the node containing the head tag for this node
   */
  public TreeGraphNode headTagNode() {
    TreeGraphNode htn = safeCast(label.get(TreeCoreAnnotations.HeadTagAnnotation.class));
    if (htn == null || (htn.treeGraph() != null && !(htn.treeGraph().equals(this.treeGraph())))) {
      return null;
    }
    return htn;
  }

  /**
   * Store the node containing the head tag for this node by
   * storing it in this node's {@link CoreLabel
   * <code>CoreLabel</code>}.  (In contrast to {@link
   * edu.stanford.nlp.ling.CategoryWordTag
   * <code>CategoryWordTag</code>}, we store head words and head
   * tags as references to nodes, not merely as
   * <code>String</code>s.)
   *
   * @param htn the node containing the head tag for this node
   */
  private void setHeadTagNode(final TreeGraphNode htn) {
    label.set(TreeCoreAnnotations.HeadTagAnnotation.class, htn);
  }

  /**
   * Safely casts an <code>Object</code> to a
   * <code>TreeGraphNode</code> if possible, else returns
   * <code>null</code>.
   *
   * @param t any <code>Object</code>
   * @return <code>t</code> if it is a <code>TreeGraphNode</code>;
   *         <code>null</code> otherwise
   */
  private static TreeGraphNode safeCast(Object t) {
    if (t == null || !(t instanceof TreeGraphNode)) {
      return null;
    }
    return (TreeGraphNode) t;
  }

  /**
   * Checks the node's ancestors to find the highest ancestor with the
   * same <code>headWordNode</code> as this node.
   */
  public TreeGraphNode highestNodeWithSameHead() {
    TreeGraphNode node = this;
    while (true) {
      TreeGraphNode parent = safeCast(node.parent());
      if (parent == null || parent.headWordNode() != node.headWordNode()) {
        return node;
      }
      node = parent;
    }
  }

  // extra class guarantees correct lazy loading (Bloch p.194)
  private static class TreeFactoryHolder {

    static final TreeGraphNodeFactory tgnf = new TreeGraphNodeFactory();

    private TreeFactoryHolder() {
    }

  }

  /**
   * Returns a <code>TreeFactory</code> that produces
   * <code>TreeGraphNode</code>s.  The <code>Label</code> of
   * <code>this</code> is examined, and providing it is not
   * <code>null</code>, a <code>LabelFactory</code> which will
   * produce that kind of <code>Label</code> is supplied to the
   * <code>TreeFactory</code>.  If the <code>Label</code> is
   * <code>null</code>, a
   * <code>CoreLabel.factory()</code> will be used.  The factories
   * returned on different calls are different: a new one is
   * allocated each time.
   *
   * @return a factory to produce treegraphs
   */
  @Override
  public TreeFactory treeFactory() {
    LabelFactory lf;
    if (label() != null) {
      lf = label().labelFactory();
    } else {
      lf = CoreLabel.factory();
    }
    return new TreeGraphNodeFactory(lf);
  }

  /**
   * Return a <code>TreeFactory</code> that produces trees of type
   * <code>TreeGraphNode</code>.  The factory returned is always
   * the same one (a singleton).
   *
   * @return a factory to produce treegraphs
   */
  public static TreeFactory factory() {
    return TreeFactoryHolder.tgnf;
  }

  /**
   * Return a <code>TreeFactory</code> that produces trees of type
   * <code>TreeGraphNode</code>, with the <code>Label</code> made
   * by the supplied <code>LabelFactory</code>.  The factory
   * returned is a different one each time.
   *
   * @param lf The <code>LabelFactory</code> to use
   * @return a factory to produce treegraphs
   */
  public static TreeFactory factory(LabelFactory lf) {
    return new TreeGraphNodeFactory(lf);
  }

  /**
   * Returns a <code>String</code> representation of this node and
   * its subtree with one node per line, indented according to
   * <code>indentLevel</code>.
   *
   * @param indentLevel how many levels to indent (0 for root node)
   * @return <code>String</code> representation of this subtree
   */
  public String toPrettyString(int indentLevel) {
    StringBuilder buf = new StringBuilder("\n");
    for (int i = 0; i < indentLevel; i++) {
      buf.append("  ");
    }
    if (children == null || children.length == 0) {
      buf.append(label.toString(CoreLabel.OutputFormat.VALUE_INDEX_MAP));
    } else {
      buf.append('(').append(label.toString(CoreLabel.OutputFormat.VALUE_INDEX_MAP));
      for (TreeGraphNode child : children) {
        buf.append(' ').append(child.toPrettyString(indentLevel + 1));
      }
      buf.append(')');
    }
    return buf.toString();
  }

  /**
   * Returns a <code>String</code> representation of this node and
   * its subtree as a one-line parenthesized list.
   *
   * @return <code>String</code> representation of this subtree
   */
  public String toOneLineString() {
    StringBuilder buf = new StringBuilder();
    if (children == null || children.length == 0) {
      buf.append(label);
    } else {
      buf.append('(').append(label);
      for (TreeGraphNode child : children) {
        buf.append(' ').append(child.toOneLineString());
      }
      buf.append(')');
    }
    return buf.toString();
  }

  public String toPrimes() {
    int copy = label().copyCount();
    return StringUtils.repeat('\'', copy);
  }

  @Override
  public String toString() {
    return label.toString();
  }

  public String toString(CoreLabel.OutputFormat format) {
    return label.toString(format);
  }

  /**
   * Just for testing.
   */
  public static void main(String[] args) {
    try {
      TreeReader tr = new PennTreeReader(new StringReader("(S (NP (NNP Sam)) (VP (VBD died) (NP (NN today))))"), new LabeledScoredTreeFactory());
      Tree t = tr.readTree();
      System.out.println(t);
      TreeGraphNode tgn = new TreeGraphNode(t, (TreeGraphNode) null);
      System.out.println(tgn.toPrettyString(0));
      EnglishGrammaticalStructure gs = new EnglishGrammaticalStructure(tgn);
      System.out.println(tgn.toPrettyString(0));
      tgn.percolateHeads(new SemanticHeadFinder());
      System.out.println(tgn.toPrettyString(0));
    } catch (Exception e) {
      System.err.println("Horrible error: " + e);
      e.printStackTrace();
    }
  }

  // Automatically generated by Eclipse
  private static final long serialVersionUID = 5080098143617475328L;

}
