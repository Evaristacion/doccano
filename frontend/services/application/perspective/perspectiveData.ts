import { perspectiveItem } from '~/domain/models/perspective/perspective'

export class PerspectiveDTO {
  id: number
  name: string
  type: string
  project: number

  constructor(item: perspectiveItem) {
    this.id = item.id
    this.project = item.project_id
    this.name = item.name
    this.type = item.type
  }
}
