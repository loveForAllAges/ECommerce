import type { AccordionItem, AccordionOptions } from 'flowbite/lib/esm/components/accordion/types';
import { AccordionInterface } from 'flowbite/lib/esm/components/accordion/interface';
declare class Accordion implements AccordionInterface {
    _items: AccordionItem[];
    _options: AccordionOptions;
    constructor(items?: AccordionItem[], options?: AccordionOptions);
    private _init;
    getItem(id: string): AccordionItem;
    open(id: string): void;
    toggle(id: string): void;
    close(id: string): void;
}
export declare function initAccordions(): void;
export default Accordion;
//# sourceMappingURL=index.d.ts.map