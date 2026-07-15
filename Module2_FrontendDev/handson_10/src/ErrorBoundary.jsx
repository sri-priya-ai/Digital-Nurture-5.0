import { Component } from "react";

export default class ErrorBoundary extends Component {
state = { hasError: false };

static getDerivedStateFromError() {
return { hasError: true };
}

componentDidCatch(err) {
console.log(err);
}

render() {
if (this.state.hasError) return <p>Something went wrong.</p>;
return this.props.children;
}
}
