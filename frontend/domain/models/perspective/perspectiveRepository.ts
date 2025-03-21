import { perspectiveItem } from '~/domain/models/perspective/perspective'

export interface PerspectiveRepository {

  list(projectId: string | number): Promise<perspectiveItem[]>

  create(projectId: string | number, item: perspectiveItem): Promise<perspectiveItem>

  update(projectId: string | number, perspectiveId: number, item: perspectiveItem): Promise<perspectiveItem>

  delete(projectId: string | number, perspectiveId: number): Promise<void>
}