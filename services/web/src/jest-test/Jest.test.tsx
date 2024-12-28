import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Link from './Jest';

it('changes the class when hovered', async () => {
    const { container } = render(<Link />);
    await userEvent.hover(screen.getByText('Link'));
    await screen.findAllByText('Link');

    // Safely check if the first child has the 'hovered' class
    const firstChild = container.firstChild as HTMLElement;
    expect(firstChild).not.toBeNull(); // Ensure it's not null
    if (firstChild) {
        expect(firstChild.classList.contains('hovered')).toBe(true);
    }
});
