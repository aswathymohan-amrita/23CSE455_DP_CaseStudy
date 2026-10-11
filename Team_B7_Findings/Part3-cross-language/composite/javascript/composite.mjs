export class Component {
    getName() {
        throw new Error("Component.getName must be implemented");
    }

    addChild(_child) {
        throw new Error("Component.addChild must be implemented");
    }

    removeChild(_child) {
        throw new Error("Component.removeChild must be implemented");
    }

    getChildren() {
        throw new Error("Component.getChildren must be implemented");
    }

    traverse() {
        throw new Error("Component.traverse must be implemented");
    }
}

export class Leaf extends Component {
    constructor(name) {
        super();
        this.name = name;
    }

    getName() {
        return this.name;
    }

    addChild(_child) {
        throw new TypeError("A location leaf cannot contain children");
    }

    removeChild(_child) {
        return false;
    }

    getChildren() {
        return [];
    }

    traverse() {
        return [this.name];
    }
}

export class Container extends Component {
    constructor(name) {
        super();
        this.name = name;
        this.children = [];
    }

    getName() {
        return this.name;
    }

    addChild(child) {
        this.children.push(child);
    }

    removeChild(child) {
        const index = this.children.indexOf(child);
        if (index < 0) {
            return false;
        }
        this.children.splice(index, 1);
        return true;
    }

    getChildren() {
        return [...this.children];
    }

    traverse() {
        return [this.name, ...this.children.flatMap((child) => child.traverse())];
    }
}
