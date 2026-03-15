//
//  ExecutionViewModel.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 8/1/23.
//

import SwiftUI
import CoreData
class ExecutionViewModel: ObservableObject {
    @Published var isSheetShowing = false
    @Published var currentField: FieldEntity?
    let managedObjectContext: NSManagedObjectContext
    var fields: [FieldEntity] = []
    var currentFieldIndex = 0
    var newExecution: ExecutionEntity?
    var actionState: ActionStateEntity?
    
    var isTextField: Bool {
        return currentField?.fieldType == "Text"
    }
    
    var isCountField: Bool {
        return currentField?.fieldType == "Count"
    }
    
    var isNumebrField: Bool {
        return currentField?.fieldType == "Number"
    }
    
    var isBoolField: Bool {
        return currentField?.fieldType == "Bool"
    }
    
    var isDateTimeField: Bool {
        return currentField?.fieldType == "Date/Time"
    }
    
    var isLocationField: Bool {
        return currentField?.fieldType == "Location"
    }

    var isUploadField: Bool {
        return currentField?.fieldType == "Upload"
    }

    var isCaptureField: Bool {
        return currentField?.fieldType == "Capture"
    }

    var isOtherField: Bool {
        return currentField?.fieldType == "Other"
    }
    

    var isListView: Bool {
        return currentField?.fieldType == "Choose from list"
    }

    // List options
    var listOptions: [String] {
        return currentField?.list?.listItems?.allObjects.compactMap { $0 as? ListItemEntity }.map { $0.name ?? "" } ?? []
    }

    init(context: NSManagedObjectContext) {
        self.managedObjectContext = context
    }

    func executeActionState(actionState: ActionStateEntity, fields: [FieldEntity]) {
        self.actionState = actionState
        print("executeActionState is called with actionState: \(actionState)")
        
        self.fields = fields
        
        // Define the function to get device's location.
        // You will need to replace this with your own location fetching mechanism.
        func getDeviceLocation() -> (latitude: Double, longitude: Double) {
            // Replace this with the actual device location fetching code
            return (0.0, 0.0)
        }

        // Create newExecution entity and set its properties
        self.newExecution = ExecutionEntity(context: managedObjectContext)
        newExecution?.id = UUID()
        let location = getDeviceLocation()
        newExecution?.latitude = location.latitude
        newExecution?.longitude = location.longitude
        newExecution?.timestamp = Date()

        if fields.count == 0 {
            // If no fields, just add the execution
            actionState.addToExecutions(newExecution!)
            try? managedObjectContext.save()
        } else {
            isSheetShowing = true
            currentField = fields.first
        }
    }
    
    func processNextField(inputValue: String) {
        // Create newFieldValue and set its properties
        let newFieldValue = FieldValueEntity(context: managedObjectContext)
        newFieldValue.id = UUID()
        newFieldValue.value = inputValue

        // Add relationships
        newExecution?.addToFieldValues(newFieldValue)
        currentField?.addToFieldValues(newFieldValue)

        // Move to the next field
        currentFieldIndex += 1
        if currentFieldIndex < fields.count {
            currentField = fields[currentFieldIndex]
        } else {
            isSheetShowing = false
            actionState?.addToExecutions(newExecution!)
            try? managedObjectContext.save()
            
            self.reset()
        }
    }
    
    func reset() {
        self.currentField = nil
        self.fields = []
        self.currentFieldIndex = 0
        self.newExecution = nil
        self.actionState = nil
    }

    // Define other functions that deal with the business logic...
}
