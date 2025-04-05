package tests

import (
	"testing"

	collections "github.com/jalusw/collections/go"
)

func TestLinkedList(t *testing.T) {
	l := collections.NewLinkedList()
	l.Append(1)
	l.Append(2)
	l.Append(3)
	l.Prepend(0)
	l.Delete(2)

	if l.Head.Data != 0 {
		t.Errorf("Expected head data to be 0, got %d", l.Head.Data)
	}
	if l.Tail.Data != 3 {
		t.Errorf("Expected tail data to be 3, got %d", l.Tail.Data)
	}

	if l.Size != 3 {
		t.Errorf("Expected size to be 3, got %d", l.Size)
	}

	if l.Head.Next.Data != 1 {
		t.Errorf("Expected second node data to be 1, got %d", l.Head.Next.Data)
	}

}
