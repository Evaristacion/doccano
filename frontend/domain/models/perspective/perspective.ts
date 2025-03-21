export class perspectiveItem {
  constructor(readonly id: number, readonly project_id: number, readonly name: string, readonly type : string) {}
  
  static create(
    project_id: number,
    name: string,
    type: string,
  ): perspectiveItem {
    return new perspectiveItem(0, project_id, name, type)
  }
}
