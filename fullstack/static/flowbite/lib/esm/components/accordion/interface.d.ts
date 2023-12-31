import { AccordionItem, AccordionOptions } from 'flowbite/lib/esm/components/accordion/types';
export declare interface AccordionInterface {
    _items: AccordionItem[];
    _options: AccordionOptions;
    getItem(id: string): AccordionItem | undefined;
    open(id: string): void;
    toggle(id: string): void;
    close(id: string): void;
}
//# sourceMappingURL=interface.d.ts.map