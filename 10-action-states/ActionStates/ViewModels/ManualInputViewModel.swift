//
//  ManualInputViewModel.swift
//  ActionStates
//
//  Created by Zachary Sturman on 7/27/23.
//

import CoreData
import Foundation

class ManualInputViewModel: ObservableObject {
    let container: NSPersistentContainer
    @Published var manualInputs = [ManualInputEntity]()
    
    init(container: NSPersistentContainer) {
        self.container = container
    }
    
    func fetchManualInputs(for actionState: ActionStateEntity) {
        manualInputs = actionState.manualInputs?.allObjects as? [ManualInputEntity] ?? []
    }
    
    
}
