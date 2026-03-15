//
//  ActionStateViewModel.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 7/29/23.
//

import Foundation
import CoreData

class ActionStateViewModel: ObservableObject {
    let managedObjectContext: NSManagedObjectContext
    var fieldViewModel: FieldViewModel

    @Published var actionStateCategory: String = "Action"
    @Published var actionStateName: String = ""
    @Published var explanation: String = ""
    @Published var collectDate: Bool = true
    @Published var collectTime: Bool = true
    @Published var collectLocation: Bool = true
    @Published var selectedTopicId: UUID?
    @Published var fieldName: String = ""

    init(context: NSManagedObjectContext) {
        self.managedObjectContext = context
        self.fieldViewModel = FieldViewModel(context: context)
    }
    
    func createActionState(fields: [InputFieldVariables]) -> Result<Bool, Error> {
        guard !actionStateName.isEmpty else {
            return .failure(NSError(domain: "", code: 100, userInfo: [NSLocalizedDescriptionKey: "Name is required"]))
        }
        
        let actionState = ActionStateEntity(context: managedObjectContext)
        actionState.id = UUID()
        actionState.category = actionStateCategory
        actionState.name = actionStateName
        actionState.explanation = explanation
        actionState.collectDate = collectDate
        actionState.collectTime = collectTime
        actionState.collectLocation = collectLocation
        
        var fieldOrder = 1
        for field in fields {
            if let fieldEntity = fieldViewModel.createField(from: field, order: Int16(fieldOrder)) {
                actionState.addToFields(fieldEntity)
                print("Added field \(fieldEntity.fieldName ?? "Unnamed Field") to ActionState")
                fieldOrder += 1
            } else {
                print("Failed to create FieldEntity for field \(field.commonAttributes.name)")
            }
        }



        do {
            try managedObjectContext.save()
            print("Saved ActionState with fields: \(String(describing: actionState.fields))")
            return .success(true)
        } catch {
            print("Failed to save ActionState: \(error)")
            return .failure(error)
        }
    }
    
    
    func populate(with actionState: ActionStateEntity) {
        actionStateCategory = actionState.category ?? "Action"
        actionStateName = actionState.name ?? ""
        explanation = actionState.explanation ?? ""
        collectDate = actionState.collectDate
        collectTime = actionState.collectTime
        collectLocation = actionState.collectLocation
    }
    
    func updateActionState(fields: [InputFieldVariables], existingActionState: ActionStateEntity?) -> Result<Bool, Error> {
        guard let existingActionState = existingActionState else {
            return .failure(NSError(domain: "", code: 100, userInfo: [NSLocalizedDescriptionKey: "ActionState not found"]))
        }
        
        existingActionState.category = actionStateCategory
        existingActionState.name = actionStateName
        existingActionState.explanation = explanation
        existingActionState.collectDate = collectDate
        existingActionState.collectTime = collectTime
        existingActionState.collectLocation = collectLocation
        
        // Delete the old fields
        if let oldFields = existingActionState.fields as? Set<FieldEntity> {
            for oldField in oldFields {
                managedObjectContext.delete(oldField)
            }
        }

        // Create and add the new fields
        var fieldOrder = 1
        for field in fields {
            if let fieldEntity = fieldViewModel.createField(from: field, order: Int16(fieldOrder)) {
                existingActionState.addToFields(fieldEntity)
                print("Added field \(fieldEntity.fieldName ?? "Unnamed Field") to ActionState")
                fieldOrder += 1
            } else {
                print("Failed to create FieldEntity for field \(field.name)")
            }
        }
        
        do {
            try managedObjectContext.save()
            print("Updated ActionState with fields: \(String(describing: existingActionState.fields))")
            return .success(true)
        } catch {
            print("Failed to update ActionState: \(error)")
            return .failure(error)
        }
    }

}
