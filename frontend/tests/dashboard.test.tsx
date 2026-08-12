import {render,screen} from '@testing-library/react'; import {VisibilityBadge} from '../src/components/VisibilityBadge'; import {describe,it,expect} from 'vitest';
describe('visibility badge',()=>{it('explains private files',()=>{render(<VisibilityBadge visibility="private"/>); expect(screen.getByText(/Only you/)).toBeInTheDocument()})})
