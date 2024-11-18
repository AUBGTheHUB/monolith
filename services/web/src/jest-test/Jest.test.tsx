import renderer, { ReactTestRendererJSON } from 'react-test-renderer';
import Link from './Jest';

it('changes the class when hovered', () => {
    const component = renderer.create(<Link />);

    let tree = component.toJSON() as ReactTestRendererJSON;
    expect(tree).toMatchSnapshot();

    // manually trigger the callback
    renderer.act(() => {
        tree.props.onMouseEnter();
    });
    // re-rendering
    tree = component.toJSON() as ReactTestRendererJSON;
    expect(tree).toMatchSnapshot();

    // manually trigger the callback
    renderer.act(() => {
        tree.props.onMouseLeave();
    });
    // re-rendering
    tree = component.toJSON() as ReactTestRendererJSON;
    expect(tree).toMatchSnapshot();
    //expect(1).toBeGreaterThan(19);
});
