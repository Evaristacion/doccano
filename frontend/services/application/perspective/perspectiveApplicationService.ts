import { PerspectiveDTO } from './perspectiveData'
import { PerspectiveRepository } from '~/domain/models/perspective/perspectiveRepository'
import { perspectiveItem } from '~/domain/models/perspective/perspective'

export class PerspectiveApplicationService {
  private repository: PerspectiveRepository

  constructor(repository: PerspectiveRepository) {
    this.repository = repository
  }

  public async list(projectId: string): Promise<PerspectiveDTO[]> {
    const items = await this.repository.list(projectId)
    return items.map((item) => new PerspectiveDTO(item))
  }

  async createPerspective(projectId: string | number, 
    data: perspectiveItem): Promise<PerspectiveDTO> {
    const createdItem = await this.repository.create(projectId, data)
    return new PerspectiveDTO(createdItem)
  }

  async updatePerspective(
    projectId: number,
    perspectiveId: number,
    data: perspectiveItem
  ): Promise<PerspectiveDTO> {
    const updatedItem = await this.repository.update(projectId, perspectiveId, data)
    return new PerspectiveDTO(updatedItem)
  }

  async deletePerspective(projectId: string | number, perspectiveId: number): Promise<void> {
    await this.repository.delete(projectId, perspectiveId)
  }
}