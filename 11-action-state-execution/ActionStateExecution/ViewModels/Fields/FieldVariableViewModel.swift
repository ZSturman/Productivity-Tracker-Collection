//
//  FieldVariableViewModel.swift
//  ActionStateExecution
//
//  Created by Zachary Sturman on 8/1/23.
//

import CoreData
import Foundation

class FieldVariableViewModel: ObservableObject {
    let managedObjectContext: NSManagedObjectContext

    // Declare your variables here. For example:
    @Published var variable: String = ""
    @Published var value: String = ""
    @Published var fieldVariables: [FieldVariableEntity] = []
    
    init(context: NSManagedObjectContext) {
        self.managedObjectContext = context
    }
    
    func updateFieldVariable(for field: FieldEntity?, with updatedField: InputFieldVariables) {
        guard let field = field else { return }

        // Create a dictionary for easier access to the updated field's properties
        let updatedFieldDict = Mirror(reflecting: updatedField).children.reduce(into: [String: Any]()) { dict, prop in
            if let label = prop.label {
                dict[label] = prop.value
            }
        }
        
        // Fetch the field variables for the field
        self.fetchFieldVariables(for: field)
        
        // Go through all possible field variables
        for (key, value) in updatedFieldDict {
            // Check if the field variable already exists
            if let fieldVar = self.fieldVariables.first(where: { $0.variable == key }) {
                // Update the value of the existing field variable
                fieldVar.value = String(describing: value)
            } else {
                // If the field variable does not exist, create a new one
                self.variable = key
                self.value = String(describing: value)
                _ = self.createFieldVariable(for: field)
            }
        }
        
        // Save the managed object context
        do {
            try self.managedObjectContext.save()
        } catch {
            print("Failed to save changes: \(error)")
        }
    }
    
    func fetchFieldVariables(for field: FieldEntity) {
        let fetchRequest: NSFetchRequest<FieldVariableEntity> = FieldVariableEntity.fetchRequest()
        fetchRequest.predicate = NSPredicate(format: "field == %@", field)

        do {
            self.fieldVariables = try managedObjectContext.fetch(fetchRequest)

            // Print the fetched field variables
            for fieldVar in self.fieldVariables {
                print("Fetched field variable: Field Name = \(fieldVar.field?.fieldName ?? ""), Variable = \(fieldVar.variable ?? ""), Value = \(fieldVar.value ?? "")")
            }

        } catch {
            print("Failed to fetch field variables: \(error)")
        }
    }

    
    
    func createFieldVariable(for field: FieldEntity) -> Result<Bool, Error> {
        guard !variable.isEmpty else {
            return .failure(NSError(domain: "", code: 100, userInfo: [NSLocalizedDescriptionKey: "Variable is required"]))
        }
        
        let fieldVariable = FieldVariableEntity(context: managedObjectContext)
        fieldVariable.id = UUID()
        fieldVariable.variable = variable
        fieldVariable.value = value
        fieldVariable.field = field

        do {
            try managedObjectContext.save()
            return .success(true)
        } catch {
            return .failure(error)
        }
    }
}

