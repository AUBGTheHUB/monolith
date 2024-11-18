const renderer = require('react-test-renderer');
const Link = require('./Jest').default;

it('changes the class when hovered', () => {
    const component = renderer.create(<Link />);
    
    let tree = component.toJSON();
    expect(tree).toMatchSnapshot();

    // manually trigger the callback
    renderer.act(() => {
        tree.props.onMouseEnter();
    });
    // re-rendering
    tree = component.toJSON();
    expect(tree).toMatchSnapshot();

    // manually trigger the callback
    renderer.act(() => {
        tree.props.onMouseLeave();
    });
    // re-rendering
    tree = component.toJSON();
    expect(tree).toMatchSnapshot();
    expect(1).toBeGreaterThan(19);
});
