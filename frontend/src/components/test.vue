<template>
  <div
    class="drag-container"
  >
    <div
      v-for="(item, index) in elements"
      :key="item.id"
      class="draggable-item"
      :style="getItemStyle(item)"
      @mousedown.stop="startDragItem($event, index)"
    >
      <p>{{ item.text }}</p>
      <!-- Button to delete item -->
      <button @click="deleteElement(item.id)">Delete</button>
    </div>
    <!-- Button to add a new item -->
    <button @click="addElement">Add Element</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      elements: [
        { id: 1, text: '元素 1', top: 100, left: 100 },
        { id: 2, text: '元素 2', top: 200, left: 200 },
        { id: 3, text: '元素 3', top: 300, left: 300 }
      ],
      dragging: false,
      currentElementIndex: null,
      offsetX: 0,
      offsetY: 0,
      containerOffsetX: 0,
      containerOffsetY: 0,
      isDraggingContainer: false
    };
  },
  methods: {
    getItemStyle(item) {
      return {
        position: 'absolute',
        top: `${item.top}px`,
        left: `${item.left}px`,
        cursor: this.dragging ? 'grabbing' : 'grab'
      };
    },

    // Start dragging a specific item
    startDragItem(event, index) {
      this.dragging = true;
      this.currentElementIndex = index;
      const element = this.elements[index];
      this.offsetX = event.clientX - element.left;
      this.offsetY = event.clientY - element.top;

      // Add global event listeners for mousemove and mouseup
      window.addEventListener('mousemove', this.dragMove);
      window.addEventListener('mouseup', this.endDrag);
      window.addEventListener('mouseleave', this.endDrag); // for mouse leaving the viewport
    },

    // Start dragging the container (empty space)
    startDragContainer(event) {
      this.isDraggingContainer = true;
      this.containerOffsetX = event.clientX - this.containerOffsetX;
      this.containerOffsetY = event.clientY - this.containerOffsetY;

      // Add global event listeners for mousemove and mouseup
      window.addEventListener('mousemove', this.dragMove);
      window.addEventListener('mouseup', this.endDrag);
      window.addEventListener('mouseleave', this.endDrag); // for mouse leaving the viewport
    },

    // During drag, update the element or container position
    dragMove(event) {
      if (this.dragging && this.currentElementIndex !== null) {
        // Dragging an element
        const element = this.elements[this.currentElementIndex];
        element.left = event.clientX - this.offsetX;
        element.top = event.clientY - this.offsetY;

        // Constrain the draggable item within the parent bounds
        const parentRect = this.$el.getBoundingClientRect();
        const minX = 0;
        const minY = 0;
        const maxX = parentRect.width - 100; // item width
        const maxY = parentRect.height - 100; // item height

        element.left = Math.max(minX, Math.min(element.left, maxX));
        element.top = Math.max(minY, Math.min(element.top, maxY));
      } else if (this.isDraggingContainer) {
        // Dragging the entire container
        const container = this.$el;
        const parentRect = container.getBoundingClientRect();
        this.containerOffsetX = event.clientX - this.containerOffsetX;
        this.containerOffsetY = event.clientY - this.containerOffsetY;

        const minX = 0;
        const minY = 0;
        const maxX = window.innerWidth - parentRect.width;
        const maxY = window.innerHeight - parentRect.height;

        this.containerOffsetX = Math.max(minX, Math.min(this.containerOffsetX, maxX));
        this.containerOffsetY = Math.max(minY, Math.min(this.containerOffsetY, maxY));

        container.style.left = this.containerOffsetX + 'px';
        container.style.top = this.containerOffsetY + 'px';
      }
    },

    // End the drag action
    endDrag() {
      if (this.dragging) {
        this.dragging = false;
        this.currentElementIndex = null;
      }

      if (this.isDraggingContainer) {
        this.isDraggingContainer = false;
      }

      // Remove global event listeners after drag ends
      window.removeEventListener('mousemove', this.dragMove);
      window.removeEventListener('mouseup', this.endDrag);
      window.removeEventListener('mouseleave', this.endDrag);
    },

    // Method to add a new element
    addElement() {
      const newElement = {
        id: this.elements.length + 1, // Unique ID for the new element
        text: `元素 ${this.elements.length + 1}`,
        top: 50, // Default position
        left: 50
      };
      this.elements.push(newElement);
    },

    // Method to delete an element
    deleteElement(id) {
      this.elements = this.elements.filter(item => item.id !== id);
    }
  }
};
</script>

<style scoped>
.drag-container {
  position: relative;
  width: 100%;
  height: 500px;
  border: 1px solid #ccc;
  background-color: #f0f0f0;
  overflow: hidden;
  cursor: grab;
}

.draggable-item {
  width: 100px;
  height: 100px;
  background-color: rgba(0, 150, 255, 0.7);
  color: white;
  text-align: center;
  line-height: 100px;
  border-radius: 8px;
  position: absolute;
  cursor: grab;
}

.draggable-item:active {
  cursor: grabbing;
}

* {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
</style>
