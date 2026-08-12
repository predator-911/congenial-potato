import {render,screen} from '@testing-library/react'; import App from '../src/App'; import {describe,it,expect} from 'vitest';
describe('auth UI',()=>{it('renders login',()=>{history.pushState(null,'','/login'); render(<App/>); expect(screen.getByText('Log in')).toBeInTheDocument()})})
