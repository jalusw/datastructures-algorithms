package collections

type Node struct {
	Data int
	Next *Node
}

type LinkedList struct {
	Head *Node
	Tail *Node
	Size int
}

func NewLinkedList() *LinkedList {
	return &LinkedList{
		Head: nil,
		Tail: nil,
		Size: 0,
	}
}

func (ll *LinkedList) Append(data int) {
	node := &Node{
		Data: data,
		Next: nil,
	}

	if ll.Head == nil {
		ll.Head = node
		ll.Tail = node
	} else {
		ll.Tail.Next = node
		ll.Tail = node
	}

	ll.Size++
}

func (ll *LinkedList) Prepend(data int) {
	node := &Node{
		Data: data,
		Next: nil,
	}

	if ll.Head == nil {
		ll.Head = node
		ll.Tail = node
	} else {
		node.Next = ll.Head
		ll.Head = node
	}

	ll.Size++
}

func (ll *LinkedList) Delete(data int) {
	if ll.Head == nil {
		return
	}

	if ll.Head.Data == data {
		ll.Head = ll.Head.Next
		ll.Size--
		return
	}

	current := ll.Head
	for current.Next != nil && current.Next.Data != data {
		current = current.Next
	}

	if current.Next != nil {
		current.Next = current.Next.Next
		if current.Next == nil {
			ll.Tail = current
		}
		ll.Size--
	}
}

func (ll *LinkedList) Search(data int) bool {
	current := ll.Head
	for current != nil {
		if current.Data == data {
			return true
		}
		current = current.Next
	}
	return false
}

func (ll *LinkedList) Traverse() {
	current := ll.Head
	for current != nil {
		print(current.Data, " ")
		current = current.Next
	}
	println()
}

func (ll *LinkedList) GetSize() int {
	return ll.Size
}
