/*
 * linked-list.js: 
 * My attempt at implementing a linked list in JavaScript
 * 2011-09-04
 *
 * By Fred Song, xx@uvic.ca
 * Public Domain.
 */

//TODO: write unit tests
(function(exports) {
    "use strict;"

    var Node = function(val) {
        this.value = val
        this.next = null;
        this.prev = null;
    };
    Node.prototype = {};

    /**
     * A doubly linked list implementation
     * @constructor
     */
    var LinkedList = function() {
        this._head = null;
        this._tail = null;
        this._size = 0;
    };

    LinkedList.prototype = {
        /**
         * Returns the number of elements in the linked list
         * @return The number of elements in the linked list
         */
        size: function() {
            return this._size;
        },

        /**
         * Add an element to the linked list
         * @param element The element to remove
         */
        add: function(el) {
            if(el === undefined || el === null) {
                throw new Exception("Invalid element");
            }
            // wrap el in node
            var node = new Node(el);

            if(!this._tail) {
                this._head = node;
                this._tail = node;
            }else {
                this._tail.next = node;
                node.prev = this._tail;
                this._tail = node;
            }
            this._size++;
        },

        /**
         * Removes an element from the linked list
         * @param element The element to remove
         */
        remove: function(el) {
            if(el === undefined || el === null) {
                throw new Exception("Invalid element");
            }
            var currNode = this._head;
            while(!currNode) {
                if(currNode.value === el) {
                    return index;
                }
                index++;
                currNode = currNode.next;
            }
            this._size--;
        },

        /**
         * Searches the linked list for an element and returns the index of its
         * first occurence in the linked list. Returns -1 if not found
         * @param element The element to search for
         * @returns Index of the first occurence of the searched element
         */
        indexOf: function(el) {
            if(el === undefined || el === null) {
                throw new Exception("Invalid element");
            }

            var currNode, i, itr;
            
            i = 0;
            itr = this.iterator();
            while(itr.hasNext()) {
                currNode = itr.next();
                if(currNode.val === el) {
                    return i;
                }
                i++;
            }

            // Element could not be found
            return -1;
        },
                 
        /**
         * Returns the element stored at a given index in the linked list
         * @param index The index of the returned element
         * @returns The element at the given index
         */
        get: function(index) {
            if(index < 0 || index >= this._size) {
                throw new Error("Index out of bounds");
            }
            var currNode, i, itr;
            
            i = 0;
            itr = this.iterator();
            while(itr.hasNext()) {
                currNode = itr.next();
                if(i === index) {
                    return currNode.val;
                }
                index++;
            }
            // Element could not be found
            return null;
        },

        /**
         * Gets an iterator object to iterate throught this linked list. The
         * iterator object has the following methods:
         *      hasNext: returns whether or not the next element exists
         *      hasPrev: returns whether or not the previous element exists
         *      next: returns the next element 
         *      prev: returns the previous element 
         * @returns Iterator object
         */
        iterator: function() {
            var currentNode = this._head;
            return {
                hasNext: function() {
                    return !!currentNode.next
                },
                hasPrev: function() {
                    return !!currentNode.prev;
                },
                next: function() {
                    if(currentNode.next) {
                        currentNode = currentNode.next;
                        return currentNode;
                    }
                    throw new Error("Element doesn't exist.");
                },
                prev: function() {
                    if(currentNode.prev) {
                        currentNode = currentNode.prev;
                        return currentNode;
                    }
                    throw new Error("Element doesn't exist.");
                }
            };
        }
    };
    
    exports.LinkedList = LinkedList;
})(window);
