import {render,screen} from '@testing-library/react'; import {UploadProgress} from '../src/components/UploadProgress'; import {describe,it,expect} from 'vitest';
describe('upload progress',()=>{it('shows percent',()=>{render(<UploadProgress p={50} speed={1000} eta={2}/>); expect(screen.getByText(/50%/)).toBeInTheDocument()})})
