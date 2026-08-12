import {formatBytes} from '../src/utils/formatBytes'; import {describe,it,expect} from 'vitest';
describe('formatBytes',()=>{it('formats megabytes',()=>expect(formatBytes(1048576)).toContain('MB'))})
